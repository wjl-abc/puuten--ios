//
//  LibViewController.h
//  puuten
//
//  Created by wang jialei on 12-8-17.
//
//

#import <UIKit/UIKit.h>
#import "ContentViewController.h"

@interface LibViewController : UIViewController<UITabBarControllerDelegate>
{
    UITabBarController *tabBarController;
}
@property (assign, nonatomic) NSString *categ;

@end
