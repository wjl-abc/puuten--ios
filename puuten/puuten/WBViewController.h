//
//  WBViewController.h
//  puuten
//
//  Created by wang jialei on 12-8-3.
//
//

#import <UIKit/UIKit.h>
#import "AFKPageFlipper.h"
@interface WBViewController : UIViewController<AFKPageFlipperDataSource>{
    AFKPageFlipper *flipper;
    NSMutableArray* viewControlerStack;
}
@property (assign, nonatomic) int wb_id;
@property (assign, nonatomic) int bs_id;
@property (assign, nonatomic) int order;
@property (assign, nonatomic) NSMutableArray *arrayData;
@property (assign, nonatomic) NSMutableDictionary *dicData;

//@property (weak, nonatomic) NSDictionary *bsdata;

@end
