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
    UIImage *clickImg;
}
@property (assign, nonatomic) int wb_id;
@property (assign, nonatomic) int bs_id;
@property (assign, nonatomic) int order;
@property (strong, nonatomic) NSMutableArray *arrayData;
@property (strong, nonatomic) NSMutableDictionary *dicData;

//@property (weak, nonatomic) NSDictionary *bsdata;

@end
