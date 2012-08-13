//
//  WBGroupViewController.h
//  puuten
//
//  Created by wang jialei on 12-8-12.
//
//

#import <UIKit/UIKit.h>

@interface WBGroupViewController : UIViewController<UITabBarControllerDelegate>
{
    UITabBarController *tabBarController;
}
@property (assign, nonatomic) int wb_id;
@end
